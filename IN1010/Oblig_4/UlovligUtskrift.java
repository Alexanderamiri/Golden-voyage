class UlovligUtskrift extends Exception{
  UlovligUtskrift(Lege person, Legemiddel middel){
    super("Legen "+ person.hentNavn()+ " har ikke lov til å skrive ut "+ middel.hentNavn());
  }
}