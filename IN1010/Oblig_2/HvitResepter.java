abstract class HvitResepter extends Resepter {
  HvitResepter(Legemiddel legemiddel, Lege utskrivendeLege, int pasientId,int reit){
    super(legemiddel, utskrivendeLege, pasientId, reit);
  }
  public String farge(){return "hvitresept";}
}
