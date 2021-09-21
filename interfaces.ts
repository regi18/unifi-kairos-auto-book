export interface AppConfig {
    username: string;
    password: string;
    fiscalCode: string;
}

export interface Lecture {
  PostoOccupato: any;
  PresenzaAula: any;
  aula: string;
  capacita: number;
  entry_id: number;
  last_minute: boolean;
  nome: string;
  note: string;
  ora_fine: string;
  ora_inizio: string;
  posto: number;
  prenotabile: boolean;
  prenotata: boolean;
}
