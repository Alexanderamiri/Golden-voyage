public abstract class Rute {
  public Rute naboost = null;
  public Rute nabovest = null;
  public Rute nabonord = null;
  public Rute nabosor = null;
  protected Labyrint lab;
  public int radnr;
  public int kolnr;
  public boolean ubrukt = false;
  public boolean aapning = false;
  Rute(int rad, int kol){
    radnr = rad;
    kolnr = kol;
  }
  public void settlaben(Labyrint labb){
    lab = labb;
  }
  public void settNabo(){
    if(radnr > 0)
      nabonord = lab.hentLabyrint()[radnr-1][kolnr];
    if(radnr < lab.radnr-1)
      nabosor = lab.hentLabyrint()[radnr+1][kolnr];
    if(kolnr > 0)
      nabovest = lab.hentLabyrint()[radnr][kolnr-1];
    if(kolnr < lab.kolnr-1)
      naboost = lab.hentLabyrint()[radnr][kolnr+1];
  }
  /*public void settnabo(){
    if (radnr==0){
      if (kolnr== 0) {
        naboost = lab.ruten[0][1];
        nabosor = lab.ruten[1][0];
      }

      else if (kolnr == lab.kolnr-1 ){
        nabovest = lab.ruten[0][lab.kolnr-1];
        nabosor = lab.ruten[1][lab.kolnr];
      }

      else{

          naboost = lab.ruten[0][kolnr+1];
          nabovest = lab.ruten[0][kolnr-1];
          nabosor = lab.ruten[1][kolnr];

      }
    }
    else if (radnr==lab.radnr-1){
      if (kolnr == 0){
        naboost = lab.ruten[radnr][1];
        nabonord = lab.ruten[radnr-1][0];
      }

      else if (kolnr == lab.kolnr-1){
        nabovest = lab.ruten[radnr][kolnr-1];
        nabonord = lab.ruten[radnr-1][kolnr];
      }
      else{
        naboost = lab.ruten[radnr][kolnr+1];
        nabovest = lab.ruten[radnr][kolnr-1];
        nabonord = lab.ruten[radnr-1][kolnr];
      }
    }
    else{
      if (kolnr == 0){
        naboost = lab.ruten[radnr][1];
        nabonord = lab.ruten[radnr-1][kolnr];
        nabosor = lab.ruten[radnr+1][kolnr];
      }

      else if (kolnr == lab.kolnr-1){
        nabovest = lab.ruten[radnr][kolnr-1];
        nabonord = lab.ruten[radnr-1][kolnr];
        nabosor = lab.ruten[radnr+1][kolnr];
      }
      else{
        naboost = lab.ruten[radnr][kolnr+1];
        nabovest = lab.ruten[radnr][kolnr-1];
        nabonord = lab.ruten[radnr-1][kolnr];
        nabosor = lab.ruten[radnr+1][kolnr];
      }
    }
  }*/
  public void finnUtvei(){gaa(this,"");}
  public abstract char tilTegn();
  public abstract void gaa(Rute ruten, String veien);
}
