/*
 * License: You are free to use any part of code in this project as long as you mention original authors of this program:
 * Alpha Team composed of: Nirmalraj JEYANATHAN Joseph - SERFATY Milan - YE Hang - ZHANG Yujia
 *
 * Supervised by Aurore (aurore.isep@gmail.com) and Hugo (myrobotswillconquertheworld@gmail.com)
 * IE.3510 (System Modeling) - ISEP 2022
 * ---------------
 *
 * GUI code for Search-and-Rescue Lego project
 *
 * This code has been made with the Processing GUI software
 * and has been converted to more common Java code to be run on all Java IDE like IntelliJ IDEA.
 * More information about the conversion in those videos:
 *  - https://vimeo.com/511923403 (Introduction)
 *  - https://vimeo.com/512164688 (float and class)
 *  - https://vimeo.com/512633151 (PImage)
 *  - https://vimeo.com/512718192 (Modern Java loops)
 *  - https://vimeo.com/512719658 (packages, colors)
 */

import processing.core.PApplet;
import processing.core.*;

import processing.net.*;

public class Main extends PApplet {
    // Communication variables
    Server myServer;
    int in_movement, sensed_object, metal, picked_up, dropped;
    int[] sensed_color = new int[3];
    int counter = 1;
    int end_of_mission = 0;

    // GUI variables
    PFont font1, font2, font3, font4, font5, font6, font7, font8, font9, font10, font11, font12, font13;  // Font is nothing but implement the words (for that pre-defintion)
    PImage escalarma1, escalarma2, escalarma3, escalarma4, escalarma5;  // Import image from the data folder
    float circlex, y = 235, z = 850;  // Ellipse data for movement x is ellipse location current (y and z are the rectangle placements of x coordinates from left side)
    float xspeed = 3;  // Fast movement speed
    float sspeed = 1;  // Small movement speed

    public static void main(String[] args) {
        PApplet.main(new String[]{Main.class.getName()});
    }

    @Override
    public void settings() {
        size(1000, 600);  // Creation of GUI outer layer
    }

    @Override
    public void setup() {
        circlex = 255;

        font1 = loadFont("./data/firstfont.vlw");  // Loading the saved font "alpha robot"
        font2 = loadFont("./data/twofont.vlw");  // Loading the saved font "legends"
        font3 = loadFont("./data/threefont.vlw");  // Loading the saved font "in movement"
        font4 = loadFont("./data/fourfont.vlw");  // Loading the saved font "sensed object"
        font5 = loadFont("./data/fivefont.vlw");  // Loading the saved font "dropped object"
        font6 = loadFont("./data/sixthfont.vlw");  // Loading the saved font "seraching object"
        font7 = loadFont("./data/seventhfont.vlw");  // Loading the saved font "sensed object"
        font8 = loadFont("./data/eighthfont.vlw");  // Loading the saved font "dropped object"
        font9 = loadFont("./data/ninthfont.vlw");  // Loading the saved font "Muster point"
        font10 = loadFont("./data/tenthfont.vlw");  // Loading the saved font "Search Pattern"
        font11 = loadFont("./data/eleventhfont.vlw");  // Loading the saved font "XXXXXXXXX reversed"
        font12 = loadFont("./data/twelethfont.vlw");  // Loading the saved font "XXXXXXXXXX reversed"
        font13 = loadFont("./data/thirteenthfloor.vlw");  // Loading the saved font "XXXXXXXX reversed"

        escalarma1 = loadImage("./data/Image1.png");  // Loading the image1 which is compatible format for processing status indicator

        myServer = new Server(this, 5204);
    }

    @Override
    public void draw() {
        background(21f, 106f, 140f);  // GUI Whole background color

        fill(252, 255, 255);  // Filling color for the text font
        textFont(font1, 32);    text("ALPHA TEAM ROBOT", 360, 36);  // Entering text for the created font and placing as per x and y cordinate
        textFont(font2, 20);    text("Legends", 60, 370);  // Defining text and where to fix
        textFont(font2, 18.5f); text("Ev3 Status indicator", 30, 236);
        textFont(font3, 18);    text("- In Movement", 50, 396);
        textFont(font4, 18);    text("- Sensed object", 50, 422);
        textFont(font11, 18);   text("- Picked object", 50, 450);
        textFont(font5, 18);    text("- Dropped object", 50, 475);

        // Ellipses used for legends, it's an indicator for robot action
        fill(246, 250, 35);  ellipse(30, 395, 20, 20);  // Placing legends color as yellow (In Movement)
        fill(240, 116, 126); ellipse(30, 420, 20, 20);  // Placing legends color as rose (Sensed object)
        fill(234, 182, 9);   ellipse(30, 445, 20, 20);  // Placing legends color as orange (Picked object)
        fill(66, 224, 114);  ellipse(30, 470, 20, 20);  // Placing legends color as green (Dropped object)


        fill(153); rect(200, 50, 700, 500);  // Placing rectangle first one after GUI size
        fill(255); rect(220, 70, 660, 460);  // Placing rectangle second one after first rectangle
        image(escalarma1, 30, 70);  // Loading the image 1 for status indicator

        fill(0);  // Filling font colour

        // Muster point box
        textFont(font9, 18); text("Muster point", 630, 410);
        fill(153); rect(510, 420, 350, 100);  // Placing rectangle which is muster box

        // Search pattern box
        fill(0);
        textFont(font10, 18); text("Search pattern", 470, 90);
        fill(153); rect(y, 120, 15, 140);  // Placing rectangle (vertical1) which is search pattern
        fill(153); rect(z, 120, 15, 140);  // Placing rectangle (vertical2) which is search pattern

        fill(50, 255, 100);  // Indicator box colour filled
        rect(30, 250, 150, 50);  // Placing fourth rectangle which is progress indication
        fill(0); //black
        ellipse(circlex, 130, 20, 30);  // Placing ellipse at entry of search pattern

        // Handle messages from Lego
        receive_msg();
        msg_actions();
    }

    public void move() {
        // Update progress indicator box
        fill(246, 250, 35);  // Indicator box colour filled
        rect(30, 250, 150, 50);  // Placing fourth rectangle which is progress indication
        fill(0); // black
        textFont(font6, 20); text("Searching object", 35, 280);

        // Make yellow ball moving at xspeed
        fill(246, 250, 35); // yellow
        ellipse(circlex, 130, 20, 30);
        circlex += xspeed;
        if (circlex >= z || circlex <= y) {
            xspeed *= -1;
        }
    }

    public void sense() {
        // Update progress indicator box for sensed object
        fill(240, 116, 126);  // Indicator box colour filled
        rect(30, 250, 150, 50);  // Placing fourth rectangle which is progress indication
        fill(0); // black
        textFont(font6, 20); text("Sensed object", 35, 280);

        // Make rose ball moving at xspeed
        fill(240, 116, 126); // rose
        ellipse(circlex, 130, 20, 30);
        circlex += sspeed;
        if (circlex >= z || circlex <= y) {
            sspeed *= -1f;
        }
    }

    public void nmobj() {
        // Update progress indicator box for non-metallic object
        fill(175, 240, 116);  // Indicator box colour filled
        rect(10, 250, 185, 50);  // Placing fourth rectangle which is progress indication
        fill(0); // black
        textFont(font6, 16); text("Non metallic object found", 14, 280);

        // Show light green ball and image
        fill(175, 240, 116); // light green
        ellipse(circlex, 130, 20, 30);
        escalarma2 = loadImage("./data/nmob1.png");
        image(escalarma2, 360, 150);  // Loading and placing the appropriate image for status indicator
    }

    public void mobj() {
        // Update progress indicator box for metallic object
        fill(234, 9, 25);  // Indicator box colour filled
        rect(10, 250, 185, 50);  // Placing fourth rectangle which is progress indication
        fill(0); // black
        textFont(font6, 16); text("Metallic object found", 18, 280);

        // Show red ball and image
        fill(234, 9, 25); // red
        ellipse(circlex, 130, 20, 30);
        escalarma3 = loadImage("./data/mobj1.png");
        image(escalarma3, 360, 150);  // Loading and placing the appropriate image for status indicator
    }

    public void pickupobj() {
        // Update progress indicator box for picked up object
        fill(234, 182, 9);  // Indicator box colour filled
        rect(10, 250, 185, 50);  // Placing fourth rectangle which is progress indication
        fill(0); // black
        textFont(font6, 16); text("Object Picked", 18, 280);

        // Show orange ball moving
        fill(234, 182, 9); // orange
        ellipse(circlex, 130, 20, 30);
    }

    public void droppedobj() {
        // Update progress indicator box for dropped object
        fill(66, 224, 114);  // Indicator box colour filled
        rect(10, 250, 185, 50);  // Placing fourth rectangle which is progress indication
        fill(0); // black
        textFont(font6, 16); text("Object dropped", 18, 280);

        // Show light green ball and image
        fill(66, 224, 114); // light green
        ellipse(circlex, 130, 20, 30);
        escalarma4 = loadImage("./data/dropobj1.png");  // Loading and placing the appropriate image for status indicator
        image(escalarma4, 550, 415);  // Loading and placing the appropriate image for status indicator
    }

    public void finaltick() {
        // Update progress indicator box for end of mission
        fill(66, 224, 114);  // Indicator box colour filled
        rect(10, 250, 185, 50);  // Placing fourth rectangle which is progress indication
        fill(0); // black
        textFont(font6, 16); text("Mission accomplished", 18, 280);

        // Show light green ball and image
        fill(66, 224, 114); // light green
        ellipse(circlex, 130, 20, 30);
        escalarma5 = loadImage("./data/final1.png");
        image(escalarma5, 280, 150);  // Loading the image 1 for status indicator
        end_of_mission = 0;
    }

    public void receive_msg() {
        // Receive message from Lego, parse it and put its data into variables
        Client client = myServer.available();
        if (client != null) {
            if (client.available() > 0) {
                // print("iteration: "); println(counter++);

                in_movement = Integer.parseInt(client.readStringUntil(10).trim());
                // println(in_movement);
                sensed_object = Integer.parseInt(client.readStringUntil(10).trim());
                // println(sensed_object);
                metal = Integer.parseInt(client.readStringUntil(10).trim());
                // println(metal);
                sensed_color[0] = Integer.parseInt(client.readStringUntil(10).trim());
                // println(sensed_color[0]);
                sensed_color[1] = Integer.parseInt(client.readStringUntil(10).trim());
                // println(sensed_color[1]);
                sensed_color[2] = Integer.parseInt(client.readStringUntil(10).trim());
                // println(sensed_color[2]);
                picked_up = Integer.parseInt(client.readStringUntil(10).trim());
                // println(picked_up);
                dropped = Integer.parseInt(client.readStringUntil(10).trim());
                // println(dropped);
                delay(10);
            }
        }
    }

    public void msg_actions() {
        // Take action after receiving new message

        if (in_movement == 1) {
            if (sensed_object == 0) {
                move();  // In movement (searching for object)
            } else {
                sense(); // Robot sensed an object
            }
        }

        if (in_movement == 0 && sensed_object == 1) {
            if (metal == 0) {
                nmobj();  // Non-metal object found
            } else if (metal == 1) {
                mobj();  // Metal object found
                // TODO: add color indicator
            }
        }

        if (picked_up == 1) {
            pickupobj();  // Picked-up metal object
        }
        if (dropped == 1) {
            droppedobj();  // Dropped metal object at muster point

            if (in_movement == 0 && end_of_mission == 1) {
                delay(3000);
                finaltick();  // Mission accomplished
            }
            end_of_mission = 1;
        }
    }

    // The serverEvent function is called whenever a new client connects.
    void serverEvent(Server server, Client client) {
        println("A new client has connected: " + client.ip());
    }
}
