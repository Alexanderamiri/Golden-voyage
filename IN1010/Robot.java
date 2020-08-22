import java.util.Random;

public class Robot implements Brukergrensesnitt{
    @Override
    public void giStatus(String status) {
        System.out.println("Here is your status");
    }

    @Override
    public int beOmKommando(String spoersmaal, String[] alternativer) {
        Random rand = new Random();
        System.out.println(spoersmaal);
        for (int i=0 ; i <= alternativer.length-1; i++){
            System.out.println(alternativer[i]);
        }
        int command = rand.nextInt(alternativer.length)+1;
        System.out.println(command);
        return command;
    }

    @Override
    public String beOmKommandoString(String spoersmaal) {
        Random gen = new Random();
        int k =  gen.nextInt(100);
        System.out.println(spoersmaal);
        String randomstring = "Robot"+k;
        System.out.println(randomstring+"\n");
        return randomstring;
    }
}
