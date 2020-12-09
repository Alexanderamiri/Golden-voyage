public class BlaaResepter extends Resepter {
  private double rabatt;
  BlaaResepter(Legemiddel legemiddel, Lege utskrivendeLege, int pasientId,int reit){
    super(legemiddel, utskrivendeLege, pasientId,reit);
    rabatt = legemiddel.hentPris()*0.25;
    }
    public String farge(){return "blåresept";}
    public double prisAaBetale(){return rabatt;}
}