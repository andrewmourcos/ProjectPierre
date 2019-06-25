import processing.video.*;
import processing.net.*; 
PImage img;

Capture video;

void captureEvent(Capture video) {
  video.read();
}

TextBox name_tbox;
TextBox phone_tbox;
 
final int stateNormal   = 0;
final int stateInputBox = 1;
final int stateVideo = 2;
int state=stateInputBox; 

int start_button;
boolean if_start = false;

// the user name 
String user_name="/"; 
String phone_num="/";
 
void setup() {
  size(1240, 680);
 
  rectMode(CORNER);
  textAlign(LEFT);
  strokeWeight(1.5);
 
  instantiateBox();
  name_tbox.isFocused = true;
  phone_tbox.isFocused = false;
  
  video = new Capture(this, 800, 450);
  //img = loadImage("test.jpg");
    
}
  
void draw() {
  background(#A6A6A6);
 
  if (state==stateNormal) {
    backgroundImage();
    textSize(32);
    text("Your name is : \n  "+user_name, 80, 80);
    text("Your phone number is : \n  "+phone_num, 80,200);
    text("Click Anywhere to Start!", 700, 200);
    
    //stroke(0);
    //rect(750,300,200,80, 3, 6, 12, 18);
    
  } else  if (state==stateInputBox) {
    //backgroundImage();
    name_tbox.display();
    phone_tbox.display();
  }
  else if (state==stateVideo) {
    video.start();
    image(video,200,0);
    //image(img,0,0);
    
    //saveStrings("user_name.txt", user_name);
    //saveStrings("phone_num.txt", phone_num);
  }
}//func
 
// ----------------------------------------------------
 
void backgroundImage() {
 
  // just a background (from the forum)
 
  int verticalNumberLines=20;
  int horizontalNumberLines=20;
  int space=5;
 
  for (int i=0; i<width; i+=width/verticalNumberLines)
  {
    for (int j=0; j<height; j+=space)
    {
      point(i, j);
    }
  }
 
  for (int j=0; j<height; j+=height/horizontalNumberLines)
  {
    for (int i=0; i<width; i+=space)
    {
      point(i, j);
    }
  }
}
 
void mouseClicked() {
 
  if (state==stateNormal) {
    // in normal mode: 
    // switch on input box
    state = stateVideo;
  } else  if (state==stateInputBox) {
    // do nothing
  }
}
 
void keyTyped() {
  if (state==stateNormal) {
    // do nothing
  } else if (state==stateInputBox) {
    //
        if (name_tbox.isFocused == true) {
            name_tbox.tKeyTyped();
        }
        else if (phone_tbox.isFocused == true) {
            phone_tbox.tKeyTyped();
        }

  }
}//func 
 
void keyPressed() {
  if (state==stateNormal) {
    //
  } else if (state==stateInputBox) {
    //
    if (name_tbox.isFocused == true) {
        name_tbox.tKeyPressed();
    }
    else if (phone_tbox.isFocused == true) {
        phone_tbox.tKeyPressed();
    }
  }
}//func
 
void instantiateBox() {
    name_tbox = new TextBox(
    "Welcome to Pierre! Please enter your name: ", 
    width/2-width/3, height/6 + height/16, // x, y
    width/3, height/2 - height/4 - height/8, // w, h
    215, // lim
    0300 << 030, color(-1, 040), // textC, baseC
    color(-1, 0100), color(#FF00FF, 0200)); // bordC, slctC
    phone_tbox = new TextBox(
    "Please enter your phone number: ", 
    width/2-width/3, height/1.5 + height/16, // x, y
    width/3, height/2 - height/4 - height/8, // w, h
    215, // lim
    0300 << 030, color(-1, 040), // textC, baseC
    color(-1, 0100), color(#FF00FF, 0200)); // bordC, slctC
}
 
// ===================================================
 
class TextBox {
 
  // demands rectMode(CORNER)
 
  final color textC, baseC, bordC, slctC;
  final short x, y, w, h, xw, yh, lim;
 
  boolean isFocused;
  String txt = "";
  String title; 
 
  TextBox(
    String tt, 
    float xx, float yy, 
    int ww, int hh, 
    int li, 
    color te, color ba, color bo, color se) {
 
    title=tt;
 
    x = (short) xx;
    y = (short) yy;
    w = (short) ww;
    h = (short) hh;
 
    lim = (short) li;
 
    xw = (short) (xx + ww);
    yh = (short) (yy + hh);
 
    textC = te;
    baseC = ba;
    bordC = bo;
    slctC = se;
  }
 
  void display() {
    stroke(isFocused? slctC : bordC);
 
    // outer 
    fill(baseC);
    rect(x-10, y-90, w+20, h+100);
 
    fill(0); 
    textSize(18);
    text(title, x, y-90+40);
 
    // main / inner
    fill(baseC);
    rect(x, y, w, h);
 
 
    fill(textC);
    textSize(16);
    text(txt + blinkChar(), x, y, w, h);
  }
 
  void tKeyTyped() {
 
    char k = key;
 
    if (k == ESC) {
      // println("esc 2");
      state=stateNormal; 
      key=0;
      return;
    } 
 
    if (k == CODED)  return;
 
    final int len = txt.length();
 
    if (k == BACKSPACE)  txt = txt.substring(0, max(0, len-1));
    else if (len >= lim)  return;
    else if (k == ENTER || k == RETURN) {
      // this ends the entering 
      if (name_tbox.isFocused ==true) {
        println("Name Entered ");
        phone_tbox.isFocused = true;
        user_name = txt;
        name_tbox.isFocused = false;
      }
      else if (phone_tbox.isFocused ==true) {
        println("Phone Entered ");
        state = stateNormal;
        phone_num = txt;
        phone_tbox.isFocused = false;
      }
    } else if (k == TAB & len < lim-3)  txt += "    ";
    else if (k == DELETE)  txt = "";
    else if (k >= ' ')     txt += str(k);
  }
 
 
  void tKeyPressed() {
    if (key == ESC) {
      println("esc 3");
      state=stateNormal;
      key=0;
    }
 
    if (key != CODED)  return;
 
    final int k = keyCode;
 
    final int len = txt.length();
 
    if (k == LEFT)  txt = txt.substring(0, max(0, len-1));
    else if (k == RIGHT & len < lim-3)  txt += "    ";
  }
 
  String blinkChar() {
    return isFocused && (frameCount>>2 & 1) == 0 ? "_" : "";
  }
 
  boolean checkFocus() {
    return isFocused = mouseX > x & mouseX < xw & mouseY > y & mouseY < yh;
  }
}
