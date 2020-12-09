public class Hovedprogrammet {
  public static void main(String[] args) throws UlovligUtskrift{
    Lege thor = new Lege("Thor");
    PreparatA Heroin = new PreparatA("Heroin",400, 2, 9 );
    PreparatB Ativan = new PreparatB("Ativan",1100,5,4);
    PreparatC Paracet = new PreparatC("Paracet", 100,500);
    Spesialist ivar = new Spesialist("ivar",42);
    Resepter ivarplis = ivar.skrivResept(Heroin,420,10);
    Militaerresepter karen = new Militaerresepter(Heroin, thor,7, 42);
    PResepter jenta = new PResepter(Paracet, thor,10,10 );
    Heroin.settNyPris(200);
    System.out.println("forventet 200 fikk : " + Heroin.hentPris());
    System.out.println("forventet 400*0.25 fikk : "+ ivarplis.prisAaBetale());
    System.out.println(ivar.toString());
    System.out.println(thor.egenId);
    System.out.println(ivar.egenId);
  }
}