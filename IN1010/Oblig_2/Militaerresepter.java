public class Militaerresepter extends HvitResepter {
  double prisabetale;
  Militaerresepter(Legemiddel legemiddel, Lege utskrivendeLege, int pasientId,int reit){
    super(legemiddel, utskrivendeLege, pasientId, reit);
    prisabetale = 0;
  }
  public double prisAaBetale(){return prisabetale;}
}
