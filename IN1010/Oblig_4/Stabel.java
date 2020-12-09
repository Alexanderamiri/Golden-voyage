public class Stabel<T> extends Lenkeliste<T> {
 public void leggPaa(T x){
   leggTil(x);
 }
 public T taAv(){
  int pos = stoerrelse()-1;
  return fjern(pos);
}
}

