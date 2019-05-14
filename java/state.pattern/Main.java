/**
 * A class description.
 * description 状态模式例子
 *
 * @author xiaowei.song
 * @version v1.0.0
 * @date 2019/04/19 19:29
 * @see "https://design-patterns.readthedocs.io/zh_CN/latest/behavioral_patterns/state.html"
 */
public class Main {
    public static void main(String[] args) {
        System.out.println("yes");
        Context ctx = new Context();
        ctx.request();
        ctx.request();
        ctx.request();
    }
}
