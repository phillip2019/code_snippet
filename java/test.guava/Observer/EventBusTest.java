package Observer;

import com.google.common.eventbus.AsyncEventBus;
import com.google.common.eventbus.DeadEvent;
import com.google.common.eventbus.EventBus;
import com.google.common.eventbus.Subscribe;
import org.junit.Assert;
import org.junit.Test;

import static java.util.concurrent.Executors.*;

public class EventBusTest {

    public class EventListener1 {
        @Subscribe
        public void subscribe(String message) {
            System.out.println("Event1: " + message);
        }
    }

    public class EventListener2 {
        @Subscribe
        public void subscribe(String message) {
            System.out.println("Event2: " + message);
        }
    }

    public class EventListener3 {
        @Subscribe
        public void subscribe(String message) {
            System.out.println("Event3: " + message);
        }
    }

    public class EventListener4 {
        @Subscribe
        public void subscribe(String message) {
            System.out.println("Event4: " + message);
        }
    }


    /**
     * 注意继承问题
     */
    public class MultipleListener {
        public String lastString;
        public Integer lastInteger;
        public Long lastLong;
        public Number lastNumber;

        @Subscribe
        public void listenString(String event) {
            System.out.println("String: " + event);
            lastString = event;
        }

        @Subscribe
        public void listenInteger(Integer event) {
            System.out.println("Integer:" + event);
            lastInteger = event;
        }

        @Subscribe
        public void listenLong(Long event) {
            System.out.println("Long:" + event);
            lastLong = event;
        }

        @Subscribe
        public void listenNumber(Number event) {
            System.out.println("Number:" + event);
            lastNumber = event;
        }

        public String getLastString() {
            return lastString;
        }

        public Number getLastNumber() {
            return lastNumber;
        }

        public Integer getLastInteger() {
            return lastInteger;
        }

        public Long getLastLong() {
            return lastLong;
        }
    }

    public class DeadEventListener {
        @Subscribe
        public void listen(DeadEvent event) {
            System.out.println(event.getEvent());
            System.out.println(event.getSource());
        }
    }

    /**
     * 测试同步事件总线
     */
    @Test
    public void testSyncEventBus() {
        EventBus eventBus = new EventBus();
        //注册事件
        eventBus.register(new EventListener1());
        //注册事件
        eventBus.register(new EventListener2());
        //注册事件
        eventBus.register(new EventListener3());
        //注册事件
        eventBus.register(new EventListener4());

//        eventBus.register(new MultipleListener());

        // 触发事件处理
        eventBus.post("hello word");

        System.out.println("Game over");
    }

    /**
     * 测试异步事件总线
     */
    @Test
    public void testAysncEventBus() {
        AsyncEventBus eventBus = new AsyncEventBus(newFixedThreadPool(3));
        eventBus.register(new EventListener1());
        eventBus.register(new EventListener2());
        eventBus.register(new EventListener3());
        eventBus.register(new EventListener4());
//        eventBus.register(new MultipleListener());
        eventBus.post("hello word");

        System.out.println("Game over");
    }

    /**
     * 测试多事件监听器
     */
    @Test
    public void testMultipleEventBus() {
        EventBus eventBus = new EventBus();
        MultipleListener multiListener = new MultipleListener();

        eventBus.register(multiListener);

        eventBus.post(new Integer(100));
        eventBus.post(new Long(800));
        String helloWorld = "hello world";
        eventBus.post(helloWorld);

        Assert.assertEquals(multiListener.getLastInteger(), new Integer(100));
        Assert.assertEquals(multiListener.getLastLong(), new Long(800L));
        Assert.assertEquals(multiListener.getLastString(), helloWorld);
    }

    /**
     * 测试Dead Event
     */
    @Test
    public void testDeadEventBus() {
        EventBus eventBus = new EventBus();

        DeadEventListener deadEventListener = new DeadEventListener();
        eventBus.register(deadEventListener);

        eventBus.post("hello word");
    }

}
