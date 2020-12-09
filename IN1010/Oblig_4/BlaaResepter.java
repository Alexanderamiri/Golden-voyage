public class BlaaResepter extends Resepter {
  private double rabatt;
  BlaaResepter(Legemiddel legemiddel, Lege utskrivendeLege, Pasient pasient,int reit){
    super(legemiddel, utskrivendeLege, pasient,reit);
    rabatt = legemiddel.hentPris()*0.25;
    }
    public String farge(){return "blåresept";}
    public double prisAaBetale(){return rabatt;}
}