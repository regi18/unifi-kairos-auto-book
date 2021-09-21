import { CookieAccessInfo } from "cookiejar";
import { readFileSync } from "fs";
import { decode } from "html-entities";
import { exit } from "process";
import req from "superagent";
import { AppConfig, Lecture } from "./interfaces";
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
    .get("https://kairos.unifi.it/auth/auth_app_test.php?response_type=token&client_id=client&redirect_uri=https://kairos.unifi.it/agendaweb/index.php?view=login&scope=openid+profile")
    .set("Referer", "https://kairos.unifi.it/agendaweb/index.php?view=login&include=login&from=logout&_lang=")
    .ok((res) => res.status < 400);

  // Posts the username and password to the login page
  const shibbolethUrl = kairosResponse?.redirects[kairosResponse?.redirects.length - 1];

  const shibbolethResponse = await agent.post(shibbolethUrl).type("form").send({
    j_username: username,
    j_password: password,
    _eventId_proceed: "",
  });

  // Parses the response html page given after the login to gather the required cookies (not the sessionid cookie)
  const respUrl = shibbolethResponse.text.match(/<form action="(.*)"\s/)?.[1];
  const relayState = shibbolethResponse.text.match('<input type="hidden" name="RelayState" value="(.*)"/>')?.[1];
  const samlResponse = shibbolethResponse.text.match('<input type="hidden" name="SAMLResponse" value="(.*)"/>')?.[1];

  // No cookies found, i.e. login failed
  if (!(respUrl && relayState && samlResponse)) return false;

  // Cookies found. Make the final request to return the actual sessionid cookie
  const finalResponse = await agent
    .post(decode(respUrl))
    .type("form")
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
async function bookLecture(id: number, fiscalCode: string): Promise<boolean> {
  const url = `https://kairos.unifi.it/agendaweb/call_ajax.php?mode=salva_prenotazioni&codice_fiscale=${fiscalCode}&id_entries=[${id}]&id_btn_element=${id}`;

  const response = await agent.get(url);
  return response.body.result === "Success";
}

/**
 *
 * @returns
 */
async function getLecturesList(): Promise<Lecture[]> {
  const url = "https://kairos.unifi.it/agendaweb/index.php?view=prenotalezione&include=prenotalezione&_lang=it";

  const response = await agent.get(url).withCredentials().set("Referer", "https://kairos.unifi.it/agendaweb/index.php?view=homepage&include=&_lang=it&login=1");

  console.log(agent.jar.getCookies(new CookieAccessInfo("kairos.unifi.it")));
  exit;
  //   console.log(response.text);

  const lecturesJson = response.text.match(/var lezioni_prenotabili = JSON.parse\('(.*)'\)/gi)?.[1];

  if (!lecturesJson) throw Error("Unable to find lectures list");

  return JSON.parse(lecturesJson)
    .map((e: { prenotazioni: []; [key: string]: any }) => e.prenotazioni)
    .flat();
}

/**
 * Main
 */
(async function () {
  // Get and parse the config file
  let config: AppConfig;
  let configRaw = readFileSync(__dirname + "/config.json").toString();
  if (configRaw) config = JSON.parse(configRaw);
  else throw Error("config.json not found. Exiting...");

  const succLogin = await login(config.username, config.password);

  if (!succLogin) {
    console.error("Login failed. Please check the credentials.");
    return;
  }

  const lecturesList = await getLecturesList();

  lecturesList.forEach((l) => {
    if (!l.prenotata && l.prenotabile) bookLecture(l.entry_id, config.fiscalCode);
  });
})();
