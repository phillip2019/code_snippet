

import java.awt.*;
import java.io.*;
import java.lang.reflect.Field;
import java.util.*;
import java.util.List;

import static com.google.common.base.MoreObjects.toStringHelper;
import static com.google.common.base.Preconditions.*;
import static java.util.Arrays.*;

public class TestOptional {
    String field1;
    String field2;
    public TestOptional() {
        this.field1 = "field1";
        this.field2 = "field2";
    }

    public static void main(String[] args) throws FileNotFoundException {
        Integer a = 6;
        Integer zero = 0;
        Optional<Integer> option = Optional.ofNullable(a);
        System.out.println(option.orElse(zero));

        checkArgument(args.length == 0);
        List<String> l = new ArrayList<>(asList("a", "b", "c", "d"));
        System.out.println(checkElementIndex(3, l.size(), "xxx"));

        TestOptional t = new TestOptional();
        System.out.println(t);

        File f = new File("/Users/xiaowei.song/opensource-workspace/code_snippet/java/lib/res/ARIALUNI.TTF");
        InputStream in = new FileInputStream(f);
        try {
            Font font = Font.createFont(Font.TRUETYPE_FONT, in);
            font.deriveFont(0);
        } catch (FontFormatException | IOException e) {
            e.printStackTrace();
        }

    }


        @Override
    public String toString() {
        Field[] fields = this.getClass().getFields();

        return toStringHelper("TestOptional")
                .add("field1", this.field1)
                .add("field2", this.field2)
                .toString();
    }
}
