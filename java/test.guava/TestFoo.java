import com.google.common.base.Function;
import com.google.common.collect.Ordering;
import com.sun.istack.internal.Nullable;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;



import static com.google.common.base.MoreObjects.*;


public class TestFoo {

    @Nullable
    String sortedBy;
    int notSortedBy;

    public TestFoo() {
    }

    public TestFoo(String sortedBy) {
        this.sortedBy = sortedBy;
    }

    public TestFoo(String sortedBy, int notSortedBy) {
        this.sortedBy = sortedBy;
        this.notSortedBy = notSortedBy;
    }

    public static void main(String[] args) {
        Ordering<TestFoo> ordering = Ordering.natural().nullsLast()
                .onResultOf(testFoo -> {
                    assert Objects.nonNull(testFoo);
                    return testFoo.sortedBy;
                });
        List<TestFoo> list = new ArrayList<>();
        list.add(new TestFoo("a"));
        list.add(new TestFoo());
        list.add(new TestFoo("b"));
        System.out.println(ordering.sortedCopy(list));
        list.sort(ordering);
        List newList = list.stream().sorted(ordering).collect(Collectors.toList());
        System.out.println(newList);
        System.out.println("hello world");
    }

    @Override
    public String toString() {
        return toStringHelper("TestFoo")
                .add("sortedBy", this.sortedBy)
                .add("notSortedBy", this.notSortedBy)
                .toString();
    }
}
