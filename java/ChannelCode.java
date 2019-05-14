
import java.lang.reflect.Field;


/**
 * 反射获取静态属性及内部静态类属性
 */
public class ChannelCode {

    /**
     * 印尼
     */
    public static final String LAZADA_CODE = "101001";
    public static final String TOKOPEDIA_CODE = "101002";

    /**
     * 印尼
     */
    public static class Indonesia {
        public static final String TRIP_GRAB_CODE = "104002";
        public static final String DS_SHOPEE_CODE = "101003";
    }

    public static void main(String[] args) {
        Class clazz = ChannelCode.class;
        // 获取对象obj的所有属性域
        Field[] fields = clazz.getDeclaredFields();
        for (Field field : fields) {
            boolean access = field.isAccessible();
            if (!access) {
                field.setAccessible(true);
            }

            //从obj中获取field变量
            Object o = null;
            String varName;
            try {
                o = field.get(clazz);
                varName = field.getName();
                System.out.println("\"" + o + "\": \"" + varName  + "\",");

                if (!access) field.setAccessible(false);
            } catch (IllegalAccessException e) {
                e.printStackTrace();
            }

        }

        Class innerClazz[] = clazz.getDeclaredClasses();
        for(Class claszInner : innerClazz){
            fields = claszInner.getDeclaredFields();
            for(Field field : fields){
                try {
                    Object o = field.get(claszInner);
                    String varName = field.getName();
                    System.out.println("\"" + o + "\": \"" + varName  + "\",");
                    //打印内容
                    /*
                    * 获取到的feild, name=version,   value=iphone6s[是手机不是吃的苹果]
                      获取到的feild, name=date,   value=生产日期 2017-06-13
                    * */
                } catch (IllegalAccessException e) {
                    e.printStackTrace();
                }

            }
        }
    }

}