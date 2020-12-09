abstract class Legemiddel {
  private static int id = -1;
  final int egenID;
  private String prepNavn;
  private double prepPris;
  private double prepVirkestoff;
  Legemiddel(String navn, double pris, double stoffmengde){
    prepNavn = navn;
    prepPris = pris;
    prepVirkestoff = stoffmengde;
    id++;
    egenID = id;
  }
  int hentId(){return egenID;}
  String hentNavn(){return prepNavn;}
  double hentPris(){return prepPris;}
  double virkestoff(){return prepVirkestoff;}
  void settNyPris(double nypris){prepPris = nypris;}
}
