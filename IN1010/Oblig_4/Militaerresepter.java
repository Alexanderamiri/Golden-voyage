public class Militaerresepter extends HvitResepter {
  double prisabetale;
  Militaerresepter(Legemiddel legemiddel, Lege utskrivendeLege, Pasient pasient,int reit){
    super(legemiddel, utskrivendeLege, pasient, reit);
    prisabetale = 0;
  }
  public double prisAaBetale(){return prisabetale;}
}
