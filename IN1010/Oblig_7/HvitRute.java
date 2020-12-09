public class HvitRute extends Rute {
  HvitRute(int rad, int kol){
    super(rad, kol);
  }
  @Override public char tilTegn(){return '.';}
  @Override public void gaa(Rute rute, String vei){
    vei += String.format("(%d, %d) --> ",kolnr,radnr);

    if(!ubrukt){
      ubrukt = true;
      if(this.aapning)
        this.gaa(rute,vei);
      nabonord.gaa(nabonord, vei);
      naboost.gaa(naboost, vei);
      nabovest.gaa(nabovest, vei);
      nabosor.gaa(nabosor, vei);
      ubrukt = false;
    }
  }
  public String toString(){return String.valueOf(tilTegn());}
}
