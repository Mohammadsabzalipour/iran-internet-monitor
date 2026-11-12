def is_criticality_balanced(tempurture, neutron_emitted):
   
    if tempurture < 800 and neutron_emitted > 500 and tempurture*neutron_emitted < 500000:
        return True
    else:
        return False
   
        
print(is_criticality_balanced(750, 600))        


def reactor_efficiency(voltage, current, theorethical_max_power):
    generated_power = voltage * current
    efficiency = generated_power / theorethical_max_power * 100 
    if efficiency >= 80:
        return "green"
    elif  60 <= efficiency < 80:
        return "orange"
    elif 30 <= efficiency < 60:
        return "red"
    else:
        return "black"
    
    
print(reactor_efficiency(200, 50, 15000))

def fail_safe(tempurture, neutrons_producted_per_second, threshold):
    x = tempurture * neutrons_producted_per_second
    lower = threshold * 0.9
    uper = threshold * 1.1
    if x < 0.9 * threshold:
        return "LOW"
    elif  lower <= x <= uper:
        return "NORMAL"
    else:
        return "DANGER"
    
print(fail_safe(tempurture=1000, neutrons_producted_per_second=30,threshold=5000))
