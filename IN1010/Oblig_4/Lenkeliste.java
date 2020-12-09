import java.util.Iterator;

public class Lenkeliste<T> implements Liste<T> {
  public Node first = null;
  public int indeks = 0;

  public class Node {

    public T data;
    public Node next;

    Node(T denne) {
      this.data = denne;
    }
  }

  public int stoerrelse() {
    int did = 0;
    Node temp = first;
    while (temp != null) {
      did++;
      temp = temp.next;
    }
    return did;
  }

  public void leggTil(int pos, T x) throws UgyldigListeIndeks {
    if (pos == 0 && stoerrelse() == 0) {
      first = new Node(x);

    }

    else if (pos > stoerrelse() || pos < 0) {
      throw new UgyldigListeIndeks(pos);
    }

    else if (pos == 0) {
      Node temp = first;
      first = new Node(x);
      first.next = temp;
    }

    else {
      Node temp = first;
      Node tempp = null;
      for (int i = 0; i < pos - 1; i++) {
        temp = temp.next;
      }
      tempp = temp.next;
      temp.next = new Node(x);
      temp.next.next = tempp;
    }

  }

  public void leggTil(T x) {

    if (first == null) {
      first = new Node(x);
    }
    else {
      Node temp = first;
      while (temp.next != null) {
        temp = temp.next;
      }
      temp.next = new Node(x);
    }
  }

  public void sett(int pos, T x) throws UgyldigListeIndeks {
    if (pos > stoerrelse() - 1 || pos < 0) {
      throw new UgyldigListeIndeks(pos);
    }
    else if (pos == 0 && stoerrelse() == 0) {
      first = new Node(x);
    }
    else if (pos == 0) {
      if (stoerrelse() == 1) {
        first = new Node(x);
      } else if (stoerrelse() > 1) {
        Node tempp = first.next;
        first = new Node(x);
        first.next = tempp;
      }
    } else {
      Node temp = first;
      Node tempp = null;
      for (int i = 0; i < pos - 1; i++) {
        temp = temp.next;
      }
      tempp = temp.next.next;
      temp.next = new Node(x);
      temp.next.next = tempp;
    }
  }

  public T hent(int pos) throws UgyldigListeIndeks {
    if (pos > stoerrelse()-1 || pos < 0) {
      throw new UgyldigListeIndeks(pos);
    }
      Node temp = first;
      for (int i = 0; i < pos; i++) {
        temp = temp.next;
      }
      return temp.data;
  }

  public T fjern(int pos) throws UgyldigListeIndeks {
    if (pos > stoerrelse()-1 || pos < 0) {
      throw new UgyldigListeIndeks(pos);
    }
    else if (pos == 0) {
      if (first.next != null) {
        T data = first.data;
        first = first.next;
        return data;
      } else {
        T data = first.data;
        first = null;
        return data;
      }
    }
    else {
      Node temp = first;
      Node tempp = first.next;
      for (int i = 0; i < pos - 1; i++) {
        temp = tempp;
        tempp = tempp.next;
      }
      T data = tempp.data;
      temp.next = tempp.next;
      return data;
    }
  }

  public T fjern() throws UgyldigListeIndeks{
    if (stoerrelse() < 1) {
      throw new UgyldigListeIndeks(-1);

    }
    else {
      T data = first.data;
      first = first.next;
      return data;
    }
  }
  public class LenkelisteIterator implements Iterator<T> {
    int index = 0;
    public boolean hasNext(){
      return (index < stoerrelse());
    }
    public T next(){
      index++;
      return hent(index-1);
    }
  }
  public Iterator iterator(){return new LenkelisteIterator();
  }
  public void test(){
    Lenkeliste<String> ll = new Lenkeliste<>();
    ll.leggTil("lol");
    ll.leggTil("ded");
    for(String kkk:ll){}

  }
}
