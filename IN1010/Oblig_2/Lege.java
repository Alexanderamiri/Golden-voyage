public class Lege {
  private String legeNavn;
  private static int legeId = 0;
  public final int egenId;
  Lege(String navn){
   legeNavn = navn;
   egenId = legeId;
   legeId++;
  }
  String hentNavn(){
    return legeNavn;}

  public Resepter skrivResept(Legemiddel legemiddel, int pasientID, int reit)
      throws UlovligUtskrift{
        if(legemiddel instanceof PreparatA) {
          throw new UlovligUtskrift(new Lege(legeNavn), legemiddel);
        }
        return new BlaaResepter(legemiddel, new Lege(legeNavn), pasientID, reit);
  }
  public String toString(){
    return "Legenavn:" + legeNavn + ",Legeid:" + egenId;
  }
}

