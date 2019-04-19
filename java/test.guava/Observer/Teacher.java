package Observer;

import java.util.Observable;
import java.util.Observer;

/**
 * @author wuyan
 */
public class Teacher implements Observer {
    private String name;

    public Teacher(String name) {
        super();
        this.name = name;
    }

    @Override
    public void update(Observable o, Object arg) {
        Student s = (Student)o;
        //获取被观察对象当前的状态
        System.out.println(String.format("%s被通知: %s正在上%s课", this.name, s.name, s.course));
    }


}
