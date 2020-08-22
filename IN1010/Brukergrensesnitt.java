public interface Brukergrensesnitt {
    void giStatus(String status);
    int beOmKommando(String spoersmaal, String[] alternativer);
    String beOmKommandoString(String spoersmaal);
}
