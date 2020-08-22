public class Gjenstand {
    public  String name;
    public int value;
    public Gjenstand (String input_name, int input_value){
         name = input_name;
         value = input_value;
    }
    public String  get_name(){return name;}
    public int get_value(){return value;}
}
