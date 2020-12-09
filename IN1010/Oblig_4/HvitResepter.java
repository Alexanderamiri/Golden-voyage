abstract class HvitResepter extends Resepter {
  HvitResepter(Legemiddel legemiddel, Lege utskrivendeLege, Pasient pasient,int reit){
    super(legemiddel, utskrivendeLege, pasient, reit);
  }
  public String farge(){return "hvitresept";}
}
