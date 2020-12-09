class SortertLenkeliste<T extends Comparable<T>>extends Lenkeliste<T> {

  @Override
  public void leggTil(T x) {
    if (stoerrelse()==0) {
      first = new Node(x);
    }
    else if (x.compareTo(first.data) <=0) {
      Node temp = new Node(x);
      temp.next = first;
      first = temp;

    }
    else {
        Node temp = first;
        Node comp = null;
        Node k = new Node(x);
        int lol;
        for (int j = 0; j < stoerrelse(); j++) {
          lol = x.compareTo(temp.data);
          if (lol > 0) {
            if (temp.next !=null) {
              comp = temp;
              temp = temp.next;
            }
            else {
              temp.next = k;
              break;
            }
          }
          else {
            k.next = temp;
            comp.next = k;
            break;
          }
        }
    }
  }
  @Override
  public T fjern(){return fjern(stoerrelse()-1);}

  @Override
  public void sett(int pos, T x) throws UnsupportedOperationException {
    throw new UnsupportedOperationException();
  }
  @Override
  public void leggTil(int pos,T x) throws UnsupportedOperationException{
    throw new UnsupportedOperationException();
  }
}