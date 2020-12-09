abstract class Resepter{
  private static int reseptId = -1;
  final int egenID;
  private int pasId = 0;
  private String legenavn;
  private int antallreit;
  private Legemiddel preparat;
  Resepter(Legemiddel legemiddel, Lege utskrivendeLege, int pasientId,int reit){
    pasId = pasientId;
    legenavn = utskrivendeLege.hentNavn();
    antallreit = reit;
    preparat = legemiddel;
    egenID = reseptId;
    reseptId++;
  }
  String hentLege(){return legenavn;}
  Legemiddel hentLegemiddel(){return preparat;}
  int hentReit(){return antallreit;}
  int hentPasientId(){return pasId;}
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
