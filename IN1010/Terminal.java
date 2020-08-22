import java.util.Scanner;
import java.util.concurrent.locks.ReentrantLock;

public class Terminal implements Brukergrensesnitt {
    Scanner choice;
    public Terminal(Scanner inputs){
        choice = inputs;
    }
    @Override
    public void giStatus(String status) {
        System.out.println("Here is your status" + status);
    }

    @Override
    public synchronized int beOmKommando(String spoersmaal, String[] alternativer) {
        synchronized (Terminal.class){
        int command = 0;
        System.out.println(spoersmaal);

        for (int i=0 ; i <= alternativer.length-1; i++){
            System.out.println(alternativer[i]);
        }
        try {command = choice.nextInt();}

        catch(Exception InputMismatchException){
            System.out.println("Wrong choice");

    }
        return command;
    }}

    @Override
    public String beOmKommandoString(String spoersmaal){
        synchronized (Terminal.class) {
            String input = new String();
            System.out.println(spoersmaal);
            try {
                input = choice.next();
            } catch (Exception InputMismatchException) {
                System.out.println("Wrong choice");
            }
            return input;
        }
    }
}
