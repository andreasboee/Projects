package studyair.studyair;

import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentTransaction;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
       displayFragment();
    }

    @Override
    protected void onStart() {
        super.onStart();
    }


    public void displayFragment(){
        //Initialize a the fragments
        AirState airStateFragment = AirState.newInstance("noe", "noe");
        OtherData otherDataFragment = OtherData.newInstance("temp", "noise", "humidity", "pressure");

        //Fragmentmanager
        FragmentManager fragmentManager = getSupportFragmentManager();
        FragmentTransaction fragTransAirState = fragmentManager.beginTransaction();

        fragTransAirState.replace(R.id.air_state_container, airStateFragment).addToBackStack("AirStateFragment").commit();

        FragmentTransaction fragTransOtherData = fragmentManager.beginTransaction();
        fragTransOtherData.replace(R.id.other_data_fragment, otherDataFragment).addToBackStack("AirStateFragment").commit();

    }
}
