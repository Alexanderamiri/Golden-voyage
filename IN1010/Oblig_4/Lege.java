public class Lege implements Comparable<Lege>{
  private String legeNavn;
  private static int legeId = 0;
  final int egenId;
  public static int nark = 0;
  public static int vann = 0;
  Lenkeliste<Resepter> resepter = new Lenkeliste<Resepter>();
  Lege(String navn){
   legeNavn = navn;
   egenId = legeId;
   legeId++;
  }

  String hentNavn(){
    return legeNavn;}

  public Resepter skrivResept(Legemiddel legemiddel, Pasient pasient, int reit) throws UlovligUtskrift{
        if(legemiddel instanceof PreparatA) {
          throw new UlovligUtskrift(new Lege(legeNavn), legemiddel);
        }
        else{
        BlaaResepter denne =  new BlaaResepter(legemiddel, new Lege(legeNavn), pasient, reit);
        utskrevederesepter().leggTil(denne);
        if (legemiddel instanceof PreparatA){
            nark++;
        }
        else if (legemiddel instanceof PreparatB){
            vann++;
        }
        return denne;}
  }
  public String toString(){
    return "Legenavn:" + legeNavn + ",Legeid:" + egenId;
  }
  private Lenkeliste<Resepter> utskrevederesepter(){
    return resepter;
  }
  public int compareTo(Lege legen){
    return legeNavn.compareTo(legen.hentNavn());
  }
}