abstract class Resepter{
  private static int reseptId = -1;
  final int egenID;
  private Pasient pasId;
  private String legenavn;
  private int antallreit;
  private Legemiddel preparat;
  Resepter(Legemiddel legemiddel, Lege utskrivendeLege, Pasient pasient,int reit){
    legenavn = utskrivendeLege.hentNavn();
    antallreit = reit;
    preparat = legemiddel;
    pasId = pasient;
    egenID = reseptId;
    reseptId++;
  }
  String hentLege(){return legenavn;}
  Legemiddel hentLegemiddel(){return preparat;}
  int hentReit(){return antallreit;}
  Pasient hentPasientId(){return pasId;}
  public boolean bruk(){
    if(antallreit>0){
      return true;
    }
    else if (antallreit<=0){
      return false;
    }
    else {
      return false;
    }
  }
  abstract public String farge();
  abstract public double prisAaBetale();
}
