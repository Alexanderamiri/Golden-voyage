public class PResepter extends HvitResepter{
  double prisabetale;
  PResepter(Legemiddel legemiddel, Lege utskrivendeLege, Pasient pasient,int reit){
    super(legemiddel, utskrivendeLege, pasient,3);
    double rabatt = 108;
    if(rabatt-legemiddel.hentPris()>0){
      prisabetale = legemiddel.hentPris()-108;
    }
    else if(rabatt-legemiddel.hentPris()<=0){
      prisabetale = 0;
    }
  }
  public double prisAaBetale(){return prisabetale;}
}
