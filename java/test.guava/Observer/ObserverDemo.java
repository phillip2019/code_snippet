package Observer;

/**
 * 传统生产者和监听者实现
 * @author wuyan
 */
public class ObserverDemo {
    public static void main(String[] args) {
        //被观察者
        Student student = new Student("杨果");
        //观察员：李老师
        Teacher teacher1 = new Teacher("李老师");
        //观察员：王老师
        Teacher teacher2 = new Teacher("王老师");
        //观察员：陈老师
        Teacher teacher3 = new Teacher("陈老师");

        //向被观察对象注册观察员
        //为学生注册观察员：李老师，王老师，陈老师
        student.addObserver(teacher1);
        student.addObserver(teacher2);
        student.addObserver(teacher3);

        student.changeState(Student.HISTORY);
        student.changeState(Student.MATH);
        student.changeState(Student.ENGLISH);
    }
}
