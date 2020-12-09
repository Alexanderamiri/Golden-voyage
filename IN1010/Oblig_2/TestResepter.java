public class TestResepter {
  public static void main(String[] args) {
   Lege fyren = new Lege("maman");
   String legenavn = fyren.hentNavn();
   PreparatA Heroin = new PreparatA("Heroin",400, 2, 9 );
   Militaerresepter blihoy = new Militaerresepter(Heroin,fyren,5,100);
   System.out.println(blihoy.prisabetale);
   System.out.println(blihoy.hentLege());
   System.out.println(blihoy.hentPasientId());
   System.out.println(blihoy.hentReit());
   System.out.println(blihoy.farge());
   System.out.println(blihoy.hentLegemiddel().virkestoff());
  }
}
