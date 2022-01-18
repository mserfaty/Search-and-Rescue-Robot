import processing.core.PApplet;
import processing.core.*;

import processing.net.*;

public class Main extends PApplet {
    // Communication
    Server myServer;
    int in_movement, sensed_object, metal, picked_up, dropped;
    int[] sensed_color = new int[3];
    int counter = 1;
    int end_of_mission = 0;

    PFont font1, font2, font3, font4, font5, font6, font7, font8, font9, font10, font11, font12, font13;//Font is nothing but implement the words (for that pre-defintion)
    PImage escalarma1; //Import image from the data folder
    PImage escalarma2; //Import image from the data folder
    PImage escalarma3; //Import image from the data folder
    PImage escalarma4; //Import image from the data folder
    PImage escalarma5; //Import image from the data folder
    float circlex, y = 235, z = 850;//elipse data for movement x is ellipse location current (y and z are the rectangle placements of x cordinate from left side)
    float xspeed = 3; //fast movement speed
    float sspeed = 1;

    public static void main(String[] args) {
        PApplet.main(new String[]{Main.class.getName()});
    }

    @Override
    public void settings() {
        size(1000, 600); //creation of GUI outer layer
    }

    @Override
    public void setup() {
        circlex = 255;
        //val = 37;

        font1 = loadFont("./data/firstfont.vlw"); //loading the saved font "alpha robot"
        font2 = loadFont("./data/twofont.vlw"); //loading the saved font "legends"
        font3 = loadFont("./data/threefont.vlw"); //loading the saved font "in movement"
        font4 = loadFont("./data/fourfont.vlw"); //loading the saved font "sensed object"
        font5 = loadFont("./data/fivefont.vlw"); //loading the saved font "dropped object"
        font6 = loadFont("./data/sixthfont.vlw"); //loading the saved font "seraching object"
        font7 = loadFont("./data/seventhfont.vlw"); //loading the saved font "sensed object"
        font8 = loadFont("./data/eighthfont.vlw"); //loading the saved font "dropped object"
        font9 = loadFont("./data/ninthfont.vlw"); //loading the saved font "Muster point"
        font10 = loadFont("./data/tenthfont.vlw"); //loading the saved font "Search Pattern"
        font11 = loadFont("./data/eleventhfont.vlw"); //loading the saved font "XXXXXXXXX reversed"
        font12 = loadFont("./data/twelethfont.vlw"); //loading the saved font "XXXXXXXXXX reversed"
        font13 = loadFont("./data/thirteenthfloor.vlw"); //loading the saved font "XXXXXXXX reversed"

        escalarma1 = loadImage("./data/Image1.png"); //loading the image1 which is compatible format for processing status indicator

        myServer = new Server(this, 5204);
    }

    @Override
    public void draw() {
        background(21f, 106f, 140f); // GUI Whole background color
        fill(252, 255, 255); //filling color for the text font
        textFont(font1, 32); //sizing of the font
        text("ALPHA TEAM ROBOT", 360, 36); //entering text for the created font and placing as per x and y cordinate
        textFont(font2, 20); //font 2 used for texting legends
        text("Legends", 60, 370); //defining text and where to fix
        textFont(font2, 18.5f);
        text("Ev3 Status indicator", 30, 236);
        textFont(font3, 18);
        text("- In Movement", 50, 396);
        textFont(font4, 18);
        text("- Sensed object", 50, 422);
        textFont(font5, 18);
        text("- Dropped object", 50, 475);
        textFont(font11, 18);
        text("- Picked object", 50, 450);

        fill(246, 250, 35); //Yellow
        ellipse(30, 395, 20, 20); //Placing legends color as yellow // ellipse used for legends, its a indicator for robot action
        fill(240, 116, 126); //green
        ellipse(30, 420, 20, 20); //Placing legends color as green
        fill(66, 224, 114); //
        ellipse(30, 470, 20, 20); //Placing legends color as red
        fill(234, 182, 9); //
        ellipse(30, 445, 20, 20); //Placing legends color as red #234, 182, 9


        fill(153);
        rect(200, 50, 700, 500); //placing rectangle first one after GUI size//
        fill(255);
        rect(220, 70, 660, 460); //placing rectangle second one after first rectangle//
        image(escalarma1, 30, 70); //loading the image 1 for status indicator
        fill(0); // filling font colour
        textFont(font9, 18);
        text("Muster point", 630, 410);
        fill(153); // Muster box colour filled
        rect(510, 420, 350, 100); //placing rectangle which is muster box//
        fill(0);
        textFont(font10, 18);
        text("Search pattern", 470, 90);
        fill(153); // search box colour filled
        rect(y, 120, 15, 140); //placing rectangle (vertical1) which is search pattern//
        fill(153); // search box colour filled
        rect(z, 120, 15, 140); //placing rectangle(vertical2) which is search pattern//
        fill(50, 255, 100); // indicator box colour filled
        rect(30, 250, 150, 50); //placing fourth rectangle which is progress indication//
        fill(0); //black
        ellipse(circlex, 130, 20, 30); //Placing ellipse at entry of search pattern

        receive_msg();
        msg_actions();
    }

    public void move() {
//        xspeed = 3;
        fill(246, 250, 35); // indicator box colour filled
        rect(30, 250, 150, 50); //placing fourth rectangle which is progress indication//
        fill(0); // black
        textFont(font6, 20);
        text("Searching object", 35, 280);
        fill(246, 250, 35); // yellow
        ellipse(circlex, 130, 20, 30);
        circlex += xspeed;
        if (circlex >= z || circlex <= y) {
            xspeed *= -1;
        }
    }

    public void sense() {
//        xspeed = 1;
        fill(240, 116, 126); // indicator box colour filled
        rect(30, 250, 150, 50); //placing fourth rectangle which is progress indication//
        fill(0); // black
        textFont(font6, 20);
        text("Sensed object", 35, 280);
        fill(240, 116, 126); // light red
        ellipse(circlex, 130, 20, 30);
        circlex += sspeed;
        if (circlex >= z || circlex <= y) {
            sspeed *= -1f;
        }
//        circlex += xspeed;
//        if (circlex >= z || circlex <= y) {
//            xspeed *= -1;
//        }
    }

    public void nmobj() {
        fill(175, 240, 116); // indicator box colour filled
        rect(10, 250, 185, 50); //placing fourth rectangle which is progress indication//
        fill(0); // black
        textFont(font6, 16);
        text("Non metallic object found", 14, 280);
        fill(175, 240, 116); // light green
        ellipse(circlex, 130, 20, 30);
        escalarma2 = loadImage("./data/nmob1.png");
        image(escalarma2, 360, 150); //loading and placing the appropriate image for status indicator
    }

    public void mobj() {
        fill(234, 9, 25); // indicator box colour filled
        rect(10, 250, 185, 50); //placing fourth rectangle which is progress indication//
        fill(0); // black
        textFont(font6, 16);
        text("Metallic object found", 18, 280);
        fill(234, 9, 25); // light green
        ellipse(circlex, 130, 20, 30);
        escalarma3 = loadImage("./data/mobj1.png");
        image(escalarma3, 360, 150); //loading and placing the appropriate image for status indicator
    }

    public void pickupobj() {
        fill(234, 182, 9); // indicator box colour filled
        rect(10, 250, 185, 50); //placing fourth rectangle which is progress indication//
        fill(0); // black
        textFont(font6, 16);
        text("Object Picked", 18, 280);
        fill(234, 182, 9); // light green
        ellipse(circlex, 130, 20, 30);
        //pending to show pickup part
    }

    public void droppedobj() {
        fill(66, 224, 114); // indicator box colour filled
        rect(10, 250, 185, 50); //placing fourth rectangle which is progress indication//
        fill(0); // black
        textFont(font6, 16);
        text("Object dropped", 18, 280);
        fill(66, 224, 114); // light green
        ellipse(circlex, 130, 20, 30);
        escalarma4 = loadImage("./data/dropobj1.png");//loading and placing the appropriate image for status indicator
        image(escalarma4, 550, 415); //loading and placing the appropriate image for status indicator
    }

    public void finaltick() {
        fill(66, 224, 114); // indicator box colour filled
        rect(10, 250, 185, 50); //placing fourth rectangle which is progress indication//
        fill(0); // black
        textFont(font6, 16);
        text("Mission accomplished", 18, 280);
        fill(66, 224, 114); // light green
        ellipse(circlex, 130, 20, 30);
        escalarma5 = loadImage("./data/final1.png");
        image(escalarma5, 280, 150); //loading the image 1 for status indicator

    }

    public void receive_msg() {
        Client client = myServer.available();
        if (client != null) {
            if (client.available() > 0) {
                print("iteration: ");
                println(counter++);

                in_movement = Integer.parseInt(client.readStringUntil(10).trim());
                println(in_movement);
                sensed_object = Integer.parseInt(client.readStringUntil(10).trim());
                println(sensed_object);
                metal = Integer.parseInt(client.readStringUntil(10).trim());
                println(metal);
                sensed_color[0] = Integer.parseInt(client.readStringUntil(10).trim());
                println(sensed_color[0]);
                sensed_color[1] = Integer.parseInt(client.readStringUntil(10).trim());
                println(sensed_color[1]);
                sensed_color[2] = Integer.parseInt(client.readStringUntil(10).trim());
                println(sensed_color[2]);
                picked_up = Integer.parseInt(client.readStringUntil(10).trim());
                println(picked_up);
                dropped = Integer.parseInt(client.readStringUntil(10).trim());
                println(dropped);
                delay(10);
            }
        }
    }

    public void msg_actions() {
        // sensed_color[]
        // Conditions when each sensors elevator level set
        // ==================
        if (in_movement == 1) {
            if (sensed_object == 0) {
                move(); //In movement (searching object)
            } else {
                sense(); // robot sensed an object
            }
        }

        if (in_movement == 0 && sensed_object == 1) {
            if (metal == 0) {
                nmobj(); //non metal object found
            } else if (metal == 1) {
                mobj(); //metal object found
                // TODO: color + update different speeds
            }
        }

        if (picked_up == 1) {
            pickupobj(); // picked up metal object
        }
        if (dropped == 1) {
            droppedobj(); // dropped metal object at muster point
//            delay(1000);
            if (in_movement == 0 && end_of_mission == 1) {
                delay(3000);
                finaltick(); // mission accomplished
            }
            end_of_mission = 1;
        }

        // ================
        //if(in_movement == 1) { // val==33
        //  move(); //In movement (serching object)
        //}
        //else{
        //  if(sensed_object == 1) { // val==34
        //    sense(); // robot sensed an object
        //    if(metal == 1) { // val==35
        //      mobj(); //metal object found
        //    }
        //    else {
        //      nmobj(); //non metal object found
        //    }
        //  }
        //}

        ////if(val==36) {
        //if(picked_up == 1) {
        //  pickupobj(); // picked up metal object
        //}
        ////if(val==36) {
        //if(dropped == 1) {
        //  droppedobj(); // dropped metal object at muster point
        //  if(in_movement == 0) {
        //    delay(1000);
        //    finaltick(); // mission accomplished
        //  }
        //}
        //if(val==37) {
        //if(in_movement == 1) {
        //  finaltick(); / mission accomplished
        //}

    }

    // The serverEvent function is called whenever a new client connects.
    void serverEvent(Server server, Client client) {
        println("A new client has connected: " + client.ip());
    }
}
