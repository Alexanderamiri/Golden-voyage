public class Aapning extends HvitRute {
  Aapning(int rad, int kol){
    super(rad, kol);
    aapning = true;
  }
  @Override public void gaa(Rute rute, String vei){
    vei += String.format("(%d, %d) \n ",kolnr,radnr);
    if (lab.hentUtskirft()) {
      lab.utvei.leggTil(vei);
    }
  }
}
