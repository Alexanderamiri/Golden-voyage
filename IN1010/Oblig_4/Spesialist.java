public class Spesialist extends Lege implements Godkjenningsfritak {
  private String navnn;
  private int kontid;
  Spesialist(String navn, int kontrollID){
    super(navn);
    navnn = navn;
    kontid = kontrollID;
  }
  @Override
  public Resepter skrivResept(Legemiddel legemiddel, Pasient pasient, int reit){
    return new BlaaResepter(legemiddel, new Lege(navnn), pasient,reit);
  }
  public int hentKontrollID(){return kontid;}
  public String toString(){
    return "Legenavn: " + navnn + ", Legeid: " + egenId+ ", kontrollId: " + kontid;
  }
}