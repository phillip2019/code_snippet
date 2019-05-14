import java.util.Objects;

/**
 * A class description.
 * description TODO
 *
 * @author xiaowei.song
 * @version v1.0.0
 * @date 2019/04/19 19:06
 */
public class ConcreteStateB implements State {

    private static State mPState;

    public ConcreteStateB() {
    }

    public static State instance() {
        if (Objects.isNull(mPState)) {
            mPState = new ConcreteStateB();
        }
        return mPState;
    }

    @Override
    public void handle(Context ctx) {
        System.out.println("doing something in State B.\n done, change state to A");
        ctx.changeState(ConcreteStateA.instance());
    }
}
