# TL21-75 
## ConnectWays
Ανάπτυξη λογισμικού στα πλαίσια εξαμηνιαίας εργασίας του 7ου εξαμήνου για το μάθημα Τεχνολογία Λογισμικού.\
Στόχος είναι η διαλειτουργικότητα μεταξύ διαφορετικών συστημάτων αυτόματης διέλευσης στα διόδια.\
Ειδικότερα, επιτρέπει στις εταιρίες διαχείρισης αυτοκινητοδρόμων να χρησιμοποιούν τους πομποδέκτες διοδίων που ανήκουν σε άλλη εταιρία,
αυξάνοντας έτσι την λειτουργικότητα των tags τους.\
Για να επιτευχθεί αυτή η συνεργασία, το λογισμικό επικοινωνεί και με τις τράπεζες.\
Τέλος, ακόμη ένας στόχος είναι η συλλογή στατιστικών δεδομένων που θα χρησιμοποιηθούν από τους συγκοινωνιακούς φορείς.

# Team
- [Panagiotis Kokkinakis](https://github.com/kokkinakis115) (AM: 03118115)
- [Christina Proestaki](https://github.com/chriproe) (AM: 03118877)
- [Marina Kontalexi](https://github.com/marinakontalexi) (AM: 03118022)
- [Kostas Mores](https://github.com/KostasMores) (AM: 03118073)
- [George Papadoulis](https://github.com/G-Papad) (AM: 03118003)

# Setup
### Requirements 
Απαιτείται να είναι εγκαταστημένη η python.\

Παρακάτω ακολουθούν τα βήματα που απαιτούνται για την εγκατάσταση.\
1. ` git clone https://github.com/ntua/TL21-75.git`
2. run setup.cmd file in TL21-75 folder

Έπειτα για να ανοίξει η εφαρμογή αρκεί να εκτελεστεί το παρακάτω αρχείο:\
3. run connectWays.cmd file in TL21-75 folder


Για να δουλέψει το API με πρωτόκολλο https είναι αναγκαία η εγκατάσταση του chocolatey.\
Αυτό γίνεται με την παρακάτω εντολή:
`@"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"`
και η παραγωγή κρυπτογραφικών κλειδιών μέσω της mkcert:
1. `choco install mkcert`
2. `mkcert -install`
3. Κατευθυνθείται στο directory TL21-75/tl2175
4. `mkcert -cert-file cert.pem -key-file key.pem 0.0.0.0 localhost 127.0.0.1 ::1`

Έπειτα για να ανοίξει η εφαρμογή αρκεί να εκτελεστεί το παρακάτω αρχείο:\
5. run connectWays_https.cmd file in TL21-75 folder
