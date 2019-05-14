import java.util.Objects;

/**
 * A class description.
 * description TODO
 *
 * @author xiaowei.song
 * @version v1.0.0
 * @date 2019/04/19 19:06
 */
public class ConcreteStateA implements State {

    private static State mPState;

    public ConcreteStateA() {
    }

    public static State instance() {
        if (Objects.isNull(mPState)) {
            mPState = new ConcreteStateA();
        }
        return mPState;
    }

    @Override
    public void handle(Context ctx) {
        System.out.println("doing something in State A.\n done, change state to B");
        ctx.changeState(ConcreteStateB.instance());
    }
}
