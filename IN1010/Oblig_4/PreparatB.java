class PreparatB extends Legemiddel {
    private int vandannendeStyrke;
    private String prepNavn;
    private double prepPris;
    private double prepVirkeStoff;
    PreparatB(String navn, double pris, double stoffmengde,int styrke){
        super(navn, pris,stoffmengde);
        vandannendeStyrke = styrke;
        prepNavn = navn;
        prepPris = pris;
        prepVirkeStoff = stoffmengde;
    }
    double hentVandannendeStyrke(){return vandannendeStyrke;}
    public String toString() {
        return "" + prepNavn+ ", " + prepPris+ ", " + hentId()+ ", " + prepVirkeStoff+ ", " + vandannendeStyrke+ ", ";
    }
}
