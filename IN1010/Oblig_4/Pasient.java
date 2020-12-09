public class Pasient implements Comparable<Pasient>{
  private static int id = 0;
  public final int egenid;
  private String navn;
  public int fødnr;
  private Stabel<Resepter> egneResepter;
  public static int nark = 0;
  public static int vann = 0;

  Pasient(int fødsellsnummer, String PasientNavn){
    egneResepter = new Stabel<Resepter>();
    fødnr=fødsellsnummer;
    navn = PasientNavn;
    egenid = id;
    id++;
  }

  public void leggTilResept(Resepter resp){
    egneResepter.leggPaa(resp);
    if (resp.hentLegemiddel() instanceof PreparatA){
      nark++;
    }
    else if (resp.hentLegemiddel() instanceof  PreparatB){
      vann++;
    }
  }

  String hentNavn(){
    return navn;}


  public Stabel<Resepter> hentReseptListe(){
    return egneResepter;
  }
  public int compareTo(Pasient pasient){
    return navn.compareTo(pasient.hentNavn());
  }
}

