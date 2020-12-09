public class SortRute extends Rute {
  SortRute(int rad, int kol){
    super(rad, kol);
  }
  @Override public char tilTegn(){return '#';}
  @Override public void gaa(Rute rute, String vei){}
  public String toString(){return  String.valueOf(tilTegn());}
}
