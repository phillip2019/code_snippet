/**
 * A class description.
 * description TODO
 *
 * @author xiaowei.song
 * @version v1.0.0
 * @date 2019/04/19 18:59
 */
public class Context {

    private State mPState;

    public State getmPState() {
        return mPState;
    }

    public void setmPState(State mPState) {
        this.mPState = mPState;
    }

    public Context() {
        // 默认初始状态为A
        mPState = ConcreteStateA.instance();
    }

    public void changeState(State st) {
        mPState = st;
    }

    public void request() {
        mPState.handle(this);
    }
}
