public class Spesialist extends Lege implements Godkjenningsfritak {
  private String navnn;
  private int kontid;
  Spesialist(String navn, int kontrollID){
    super(navn);
    navnn = navn;
    kontid = kontrollID;
  }
  @Override
  public Resepter skrivResept(Legemiddel legemiddel, int personid, int reit){
    return new BlaaResepter(legemiddel, new Lege(navnn), personid,reit);
  }
  public int hentKontrollID(){return kontid;}
  public String toString(){
    return "Legenavn: " + navnn + ", Legeid: " + egenId+ ", kontrollId: " + kontid;
  }
}