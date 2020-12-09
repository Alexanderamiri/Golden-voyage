public class TestPreparat {
  public static void main(String[] args) {
    PreparatA Heroin = new PreparatA("Heroin",400, 2, 9 );
    PreparatB Ativan = new PreparatB("Ativan",1100,5,4);
    PreparatC Paracet = new PreparatC("Paracet", 100,500);
    System.out.println(Paracet.hentId());
    System.out.println(Ativan.hentId());
    System.out.println(Heroin.hentId());
    System.out.println(Paracet.hentNavn());
    System.out.println(Ativan.hentNavn());
    System.out.println(Heroin.hentNavn());
    System.out.println(Paracet.hentPris());
    System.out.println(Ativan.hentPris());
    System.out.println(Heroin.hentPris());
    System.out.println(Ativan.hentVandannendeStyrke());
    System.out.println(Heroin.hentNarkotiskStyrke());
    System.out.println(Heroin.toString());
  }
}
