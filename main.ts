import req from 'superagent';
import { decode } from 'html-entities';
import { CookieAccessInfo } from 'cookiejar';
import { readFileSync } from 'fs';
import { AppConfig } from './interfaces';
const agent = req.agent();

/**
 * Logs into the 'Kairos Agenda Web' UniFi service
 * If the login is successful, a cookie will be used from here on when
 * making requests (that is automatically handled by superagent)
 *
 * @param username The matricola
 * @param password The password
 * @returns True if login was successful, false otherwise
 */
async function login(username: string, password: string): Promise<boolean> {
    // Requests the login page
    const kairosResponse = await agent
        .get(
            'https://kairos.unifi.it/auth/auth_app_test.php?response_type=token&client_id=client&redirect_uri=https://kairos.unifi.it/agendaweb/index.php?view=login&scope=openid+profile'
        )
        .set(
            'Referer',
            'https://kairos.unifi.it/agendaweb/index.php?view=login&include=login&from=logout&_lang='
        )
        .ok((res) => res.status < 400);

    // Posts the username and password to the login page
    const shibbolethUrl =
        kairosResponse?.redirects[kairosResponse?.redirects.length - 1];

    const shibbolethResponse = await agent
        .post(shibbolethUrl)
        .type('form')
        .send({
            j_username: username,
            j_password: password,
            _eventId_proceed: '',
        });

    // Parses the response html page given after the login to gather the required cookies (not the sessionid cookie)
    const respUrl = shibbolethResponse.text.match(/<form action="(.*)"\s/)?.[1];
    const relayState = shibbolethResponse.text.match(
        '<input type="hidden" name="RelayState" value="(.*)"/>'
    )?.[1];
    const samlResponse = shibbolethResponse.text.match(
        '<input type="hidden" name="SAMLResponse" value="(.*)"/>'
    )?.[1];

    // No cookies found, i.e. login failed
    if (!(respUrl && relayState && samlResponse)) return false;

    // Cookies found. Make the final request to return the actual sessionid cookie
    const finalResponse = await agent
        .post(decode(respUrl))
        .type('form')
        .send({
            RelayState: decode(relayState),
            SAMLResponse: decode(samlResponse),
        });

    return true;
}

/**
 * Books a lecture
 *
 * @param id The lecture's id
 * @param fiscalCode The fiscal code of the student that wants to book the lecture
 * @returns True if successful, false otherwise
 */
async function bookLecture(id: string, fiscalCode: string): Promise<boolean> {
    const url = `https://kairos.unifi.it/agendaweb/call_ajax.php?mode=salva_prenotazioni&codice_fiscale=${fiscalCode}&id_entries=[${id}]&id_btn_element=${id}`;

    const response = await agent.get(url);
    return response.body.result === 'Success';
}

/**
 *
 * @returns
 */
async function getLecturesList(): Promise<Lecture[]> {
    // ! P.S. The tests below were done on &include=prenotalezione_gestisci, don't know if it's the same

    const url =
        'https://kairos.unifi.it/agendaweb/index.php?view=prenotalezione&include=prenotalezione&_lang=it#';

    // ! Without the manual cookie header the php wont't return the lecture list
    // ? It only needs the cookie "_opensaml_req_ss" and "PHPSESSID"
    const response = await agent.get(url).withCredentials();
    // .set({
    //     cookie: '_opensaml_req_ss%3Amem%3A94c72510a67695953bf82d9eb7a826d317aec1f77588c9c3cb32ab4b4cb42f2f=_56e09a71cada64ad86da6530a9c08b96; PHPSESSID=a41gg9dncek6t6m31rinescgr1;',
    // });

    // ! The cookiejar doesn't have "_opensaml_req_ss", that's why it doesn't work
    // console.log(agent.jar.getCookies(new CookieAccessInfo('kairos.unifi.it')));
    // console.log(response.text);
    
    const lecturesJson = response.text.match(/var lezioni_prenotabili = JSON.parse\('(.*)'\)/gi)?.[1];

    if (!lecturesJson) throw Error("Unable to find lectures list");

    return JSON.parse(lecturesJson)
        .map((e) => e.prenotazioni)
        .flat();
}

/**
 * Main
 */
(async function () {
    // Get and parse the config file
    let config: AppConfig;
    let configRaw = readFileSync(__dirname + '/config.json').toString();
    if (configRaw) config = JSON.parse(configRaw);
    else throw Error('config.json not found. Exiting...');

    const succLogin = await login(config.username, config.password);

    if (!succLogin) {
        console.error('Login failed. Please check the credentials.');
        return;
    }

    const lecturesList = await getLecturesList();
    
    lecturesList.forEach((l) => {
        if (!l.prenotata && l.prenotabile) bookLecture(l.entry_id, config.fiscalCode);
    });
})();
