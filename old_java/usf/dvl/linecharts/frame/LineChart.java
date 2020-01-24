package usf.dvl.linecharts.frame;

import processing.core.PApplet;
import processing.core.PConstants;
import usf.dvl.draw.DFrame;
import usf.dvl.signal.Signal; 
import usf.dvl.signal.SignalDerivative;
import usf.dvl.signal.SignalDifference;

public class LineChart extends DFrame {

	public static boolean pointsOn = false;
	public static boolean toggleText = true;

	boolean selected = false;
	boolean hovered = true;

	float maxX, minX;
	int   pointSize = 5;
	float lineWeight = 1;
	float maxValue, minValue;
	float pointStrokeWeight = 1;

	int lineColor        = 0;
	int pointStrokeColor = 0;
	int pointFillColor   = 0;
	int pointMinColor    = 0;
	int pointMaxColor    = 0;


	public LineChart(PApplet p){
		super(p);

		lineColor        = papplet.color(0);
		pointStrokeColor = papplet.color(0);
		pointFillColor   = papplet.color(0);
		pointMinColor    = papplet.color(0,0,255);
		pointMaxColor    = papplet.color(255,0,0);

	}


	void setPointSize(int _ps){
		pointSize = _ps;
	}

	int getPointSize(){
		if( pointsOn )  return 0;
		return pointSize;
	}

	Signal  og=null, points=null;
	SignalDerivative derv=null;
	SignalDifference diff=null;
	
	void setData( Signal _og, Signal _points  ){
		og = _og;
		points = _points;
		maxValue = og.getMaxY();
		minValue = og.getMinY();
		maxX = points.size()-1;
		minX = 0; 
		derv = new SignalDerivative( points );
		diff = new SignalDifference( og, points );
	}


	//void draw( PointContainer og, PointContainer points ){
	public void draw(   ){
		papplet.stroke( 0 );
		papplet.noFill();

		// account for hovering
		if( mouseInside() ){
			papplet.strokeWeight(2.5f);
			hovered = true;
		}
		else{
			papplet.strokeWeight(1.5f);
			hovered = false;
		}
		papplet.rect(u0, v0, w, h);

		//drawError( og, points );

		/* connect each point by line */
		papplet.strokeWeight(lineWeight);

		// draw the lines
		papplet.stroke(lineColor); drawLine( points, minValue, maxValue );
		//papplet.stroke(255,0,0);   drawLine( diff,   (minValue-maxValue)/2, (maxValue-minValue)/2 );
		//papplet.stroke(0,0,255);   drawLine( derv,   (minValue-maxValue)/2, (maxValue-minValue)/2 );

		
		if( pointsOn ) {
			papplet.strokeWeight(pointStrokeWeight);
			papplet.stroke(pointStrokeColor);
	
			for( int i = 0; i < points.size(); i++) {
				if(colorMax( points, i ) == 1){
					papplet.fill(pointMaxColor);
				}else if(colorMin( points, i ) == 1){
					papplet.fill(pointMinColor);
				}else {
					papplet.fill(pointFillColor);
				}
	
				float xPos = PApplet.map( i, minX, maxX, u0, u0+w );
				float yPos = PApplet.map( points.get(i), minValue, maxValue, v0+h-20, v0+20 );
	
				int ptSz = getPointSize();
				papplet.ellipse(xPos, yPos, ptSz, ptSz);
			}
		}

		if( toggleText ) {
			papplet.stroke(0);
			papplet.fill(0);
			papplet.textAlign(PConstants.LEFT);
			papplet.text( points.graphType(), u0+5, v0+15 );
		}
	}
	
	private void drawLine( Signal pc, float yMin, float yMax ) {
		float uMin = yMin;
		float uMax = yMax;
		if( yMin == yMax ) uMin -= 1;
		if( yMin == yMax ) uMax += 1;
		for(int i = 0; i < pc.size()-1; i++ ) {
			float xPos0 = PApplet.map( i, minX, maxX, u0, u0+w );
			float yPos0 = PApplet.map( PApplet.constrain( pc.get(i), uMin, uMax), uMin, uMax, v0+h-20, v0+20 );
			float xPos1 = PApplet.map( i+1, minX, maxX, u0, u0+w );
			float yPos1 = PApplet.map( PApplet.constrain( pc.get(i+1), uMin, uMax), uMin, uMax, v0+h-20, v0+20 );			
			papplet.line(xPos0, yPos0, xPos1, yPos1);
		}
		
	}

	public boolean mousePressed(){
		if( mouseInside() ) {  
			selected = !selected; 
			return true; 
		}
		return false;
	}


	/*  Both color functions below control the color of the points if points are turned on */
	public int colorMax(Signal pt,int i){
		/* 0 - false */
		try{
			float curr = pt.get(i);
			if(i == 0){
				float r_n = pt.get(i+1);
				if(curr > r_n)
					return 1;
				else
					return 0;
			}else if( i == pt.size()-1){
				float l_n = pt.get(i-1);
				if(curr > l_n)
					return 1;
				else
					return 0;
			}else {
				float l_n = pt.get(i-1);
				float r_n = pt.get(i+1);
				if(l_n < curr && r_n < curr){
					return 1;
				} else{
					return 0;
				}
			}
		}catch(Exception e){
			e.printStackTrace();
		}
		return 0;
	}

	public int colorMin(Signal pt, int i){
		try {
			float curr = pt.get(i);
			if(i == 0){
				float r_n = pt.get(i+1);
				if(curr < r_n)
					return 1;
				else
					return 0;
			}else if( i == pt.size()-1){
				float l_n = pt.get(i-1);
				if(curr < l_n)
					return 1;
				else
					return 0;
			}else {
				float l_n = pt.get(i-1);
				float r_n = pt.get(i+1);
				if(l_n > curr && r_n > curr){
					return 1;
				} else{
					return 0;
				}
			}
		}catch(Exception e){
			e.printStackTrace();
		}
		return 0;
	}
}