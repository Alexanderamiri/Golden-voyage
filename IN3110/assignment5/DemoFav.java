import java.io.File;
class DemoFav{
    public static void main(String []args){
        System.out.println("How old are you?");
        int age = 22;
        //Some comment blablabla
        System.out.println("Are you a student?");
        String studentOrNot = 'Yes';
        student(age, studentOrNot);
        int sum = sum(age);
        System.out.println(sum);
        String i = null;
        Boolean b = true;
        Navn nyttNavn = new Navn("Alex");
        System.out.println("You're name is stupid dude, who even calls them selves for : " + nyttNavn.getname() );
    }
    static void student( int age, String ans) {
        if ((age >= 18) && (age <= 30) && (ans.equalsIgnoreCase("Yes"))){
            System.out.println("");

        }else if(ans.equalsIgnoreCase("No")){
            System.out.println("You're missing out");

        }else{
            System.out.println("Sorry error ");
        }
    }
    static int sum(int num){
        int sum = 0, i = 0;
        while( num != 0 && i < 10 ) {
            sum += num;
            num += 1;
            i++;
            if(sum > 500){
                break;
            }
        }
        return sum;
    }
}
class name{
    private String name;
    public Navn(String name){
        this.name = name;
    }
    public String getname(){
        return this.name;
    }
}
  