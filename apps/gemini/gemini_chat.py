from google import genai
import os

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

SYSTEM_PROMPT = """You are 'Airport Apex', a smart, empathetic, and welcoming digital assistant for a modern airport. 
Your goal is to make every customer's journey as comfortable, fast, and stress-free as possible.

Your main rules:
1. Tone: Professional, yet warm and human. You are happy to help.
2. Expertise: You assist with flight schedules, bookings, baggage rules, terminal navigation, and airport services.
3. Flexibility (Small Talk): If a user greets you, asks how you are, or makes a joke — engage in the conversation politely and briefly, but immediately steer it back to offering your airport-related services. 
4. Boundaries of Competence: If a question is completely unrelated to travel/aviation (e.g., politics, programming, recipes), politely state that your specialty is the sky and airplanes, and offer to find a flight instead.
5. Conciseness: Answer briefly and to the point. Do not write huge walls of text.
"""

def get_flight_status(flight_number: str) -> str:
    """Returns the status of a flight given its number."""

    try:
        from flights.models import Flight
        flight = Flight.objects.select_related('departure_airport', 'arrival_airport').get(flight_number__iexact=flight_number)
        return (f"Flight {flight.flight_number}. "
                f"Route: {flight.departure_airport.city} -> {flight.arrival_airport.city}. "
                f"Status: {flight.get_status_display()}. "
                f"Departure: {flight.departure_time.strftime('%Y-%m-%d %H:%M')}.")
        
    except Exception as e:
        print(f"Error fetching flight status: {str(e)}")
        return f"Sorry, I couldn't find any information about flight {flight_number}."

def get_departure_board(departure_airport_city: str, arrival_airport_city: str) -> str:
    """Returns the departure board for a given airport. If givven any city, ask for another one."""
    
    try:
        from flights.models import Flight
        flights = Flight.objects.select_related('departure_airport', 'arrival_airport').filter(
            departure_airport__city__iexact=departure_airport_city,
            arrival_airport__city__iexact=arrival_airport_city
        ).order_by('departure_time')[:5] 
        if not flights:
            return f"No upcoming flights found from {departure_airport_city} to {arrival_airport_city}."

        response = f"Departure board for {departure_airport_city} to {arrival_airport_city}:\n"
        for flight in flights:
            response += (f"- Flight {flight.flight_number} to {flight.arrival_airport.city} at "
                         f"{flight.departure_time.strftime('%Y-%m-%d %H:%M')} - Status: {flight.get_status_display()}\n")

    except Exception as e:
        print(f"Error fetching departure board: {str(e)}")
        return f"Sorry, I couldn't retrieve the departure board for {departure_airport_city} to {arrival_airport_city} at the moment."


def get_flight_prices(flight_number: str) -> str:
    """Returns the minimum price for each seat class (economy, business, first) for a given flight number."""
    
    try:
        from django.db.models import Min, Count
        from bookings.models import Seat
        seat_stats = Seat.objects.filter(
            flight__flight_number__iexact=flight_number
        ).values('seat_class').annotate(
                min_price=Min('price'),
                available_seats=Count('id')
            )
        
        if not seat_stats:
            return f"Sorry, I couldn't find any information about seats on flight {flight_number} or all tickets are sold out."
        
        results = [f"Available tickets for flight {flight_number}:"]
        class_names = {'economy': 'Economy', 'business': 'Business', 'first': 'First Class'}
        
        for stat in seat_stats:
            class_display = class_names.get(stat['seat_class'], stat['seat_class'])
            results.append(f"- {class_display}: from {stat['min_price']} (available seats: {stat['available_seats']})")
            
        return "\n".join(results)
        
    except Exception as e:
        print(f"Error fetching flight prices: {str(e)}")
        return f"Sorry, I couldn't retrieve price information for flight {flight_number} at the moment."

def ask_ai():
    try:
        return client.chats.create(
            model="gemini-2.5-flash",
            config=genai.types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.3,
                tools=[
                    get_flight_status,
                    get_departure_board,
                    get_flight_prices
                ]
            )
        )
    except Exception as e:
        print(f"Error initializing AI chat session: {str(e)}")
        return f"Error: {str(e)}"