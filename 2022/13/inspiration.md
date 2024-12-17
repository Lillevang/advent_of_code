This Java solution could probably be ported to crystal? Parsing the input as json is a pretty good idea...


```java
import com.google.gson.Gson;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Scanner;

public class BilinearInterpolation2 {
    public static void main(String[] args) throws FileNotFoundException {

        Scanner scan = new Scanner(new File("src/main/java/input.txt"));

        Gson gson = new Gson();

        ArrayList<Object> finals = new ArrayList<>();
        while(scan.hasNextLine()){
            String s = scan.nextLine();
            if(s.length()==0) continue;;
            ArrayList object1 = gson.fromJson(s, ArrayList.class);
            finals.add(object1);
        }
        finals.sort(BilinearInterpolation2::compare);
        int index = 0, a = 0, b = 0;
        for(Object ob : finals){
            if(ob.toString().equals("[[2.0]]")) a = index;
            if(ob.toString().equals("[[6.0]]")) b = index;
            index++;
        }
        System.out.println((a+1) * (b+1));
    }

    public static int compare(Object a, Object b){
        if(a instanceof Double && b instanceof Double){
            return Double.compare((Double) a, (Double) b);
        }
        if(a instanceof ArrayList && b instanceof ArrayList){
            for(int i = 0;i<Math.min(((ArrayList<?>) a).size(), ((ArrayList<?>) b).size());i++){
                int v = compare(((ArrayList<?>) a).get(i), ((ArrayList<?>) b).get(i));
                if(v == -1 || v == 1) return v;
            }
            return Integer.compare(((ArrayList<?>) a).size(), ((ArrayList<?>) b).size());
        }
        ArrayList<Object> newA = new ArrayList<>();
        if(a instanceof ArrayList && b instanceof Double){
            newA.add(b);
            return compare(a, newA);
        }else{
            newA.add(a);
            return compare(newA, b);
        }

    }

}
```