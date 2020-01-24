package usf.dvl.signal.filters;

public abstract class CachedFloat {

	private boolean computed = false;
	private float val = Float.NaN; 
	
	protected abstract float compute();
	
	public float getValue() {
		if( !computed ) val = compute();
		return val;
	}

}
