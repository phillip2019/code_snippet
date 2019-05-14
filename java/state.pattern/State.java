/**
 * A class description.
 * description TODO
 *
 * @author xiaowei.song
 * @version v1.0.0
 * @date 2019/04/19 19:03
 */

public interface State {
    /**
     * 当状态改变时，更改行为
     */
    void handle(Context ctx);
}
