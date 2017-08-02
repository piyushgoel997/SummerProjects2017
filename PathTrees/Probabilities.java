import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Scanner;

/**
 * Created by Piyush on 6/1/2017.
 */
public class Probabilities {
    public static final String PATH = "C:\\Users\\Piyush.CPU223\\Desktop\\New folder\\alarms.txt";
    public static final int X = 1024;

    public static void main(String[] args) {
        Scanner s = null;
        try {
            s = new Scanner(new File(PATH));
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
        int ctx = 0; //count of X
        ArrayList<Integer> al = new ArrayList<>();
        while(s.hasNextInt()) {
            int temp = s.nextInt();
            if(temp == 441 || temp == 442) { // replace 441 and 442 by X(= 1024)
                temp = X;
                ctx++;
            }
            al.add(temp);
        }
        System.out.println("al made");
        Trees<Integer> trees = new Trees<>(al, X, 4); // limit = no of terms in the path we consider at once.
        System.out.println("trees made");
        ArrayList probabilities = trees.probabilityList();
        for (int i = 0; i < probabilities.size(); i++) {
            System.out.println(probabilities.get(i));
        }
        System.out.println();
    }
}
